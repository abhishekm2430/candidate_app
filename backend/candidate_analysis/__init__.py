from .framework import create_app
app = create_app()


#[-] Rename app to candidate_analysis
#[-] Try to move migrations inside app root folder
#[-] Add all the table schema
#[ ] Fix the issue: AttributeError: 'CandidateDocumentKeyword' object has no attribute 'foreign_keys'
#[ ] Check into file uploading plugin or flask api
#[ ] Check into public folder where file will be stored
#[ ] Explore into instance_relative_config while initialising app
