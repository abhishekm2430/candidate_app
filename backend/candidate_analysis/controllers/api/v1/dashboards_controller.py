import functools
import os
import time
import sys
from flask import Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from candidate_analysis.models import User
from werkzeug.utils import secure_filename
from candidate_analysis.lib.storage_utils import FileStorage
from flask_cors import CORS, cross_origin
from candidate_analysis.models import CandidateDocument
from candidate_analysis.models import CandidateDocumentKeyword
from candidate_analysis.framework.db import db

sys.path.append('/home/abhishek/candidate-analysis/candidate_analysis/backend/tasks')
from celery_tasks import grammar_score_calculation, keyword_density_calculation

blueprint = Blueprint('dashboards_controller', __name__, url_prefix='/api/v1/dashboards')


@blueprint.route('/resume_analysis', methods=['POST'])
#@jwt_required
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    file_saver = FileStorage(file, at='resume')

    file_path = file_saver.save_file()
    if(file_path):
        doc = CandidateDocument(document_path = file_path, candidate_id = 1)
        db.session.add(doc)
        db.session.commit()
        grammar_score_calculation.apply_async(args = [doc.candidate_document_id])
        keyword_density_calculation.apply_async(args = [doc.candidate_document_id])
        return jsonify({"message": "your resume is uploaded successfully", "document_id": doc.candidate_document_id}), 200
    else:
        return jsonify({ "message": "operation failed" }), 406


@blueprint.route('/candidate_data/<document_id>', methods=['GET'])
#@jwt_required
def get_document_details(document_id):
    doc = CandidateDocument.query.filter_by(candidate_document_id = document_id).first()
    if(doc == None):
        return jsonify({ "message": "No such document exist"}), 406
    doc_score = doc.grammar_score
    if(doc.grammar_score == None):
        return jsonify({ "message": "Please wait, analysis is going on"}), 200
    keyword_density_info = CandidateDocumentKeyword.get_document_keywords_density(document_id)
    return jsonify({"message": "Analysis completed successfully", "density": keyword_density_info, "grammar_score": doc_score}), 200

    


