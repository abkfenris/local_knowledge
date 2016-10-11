#!/usr/bin/env python

import os
import logging

from local_knowledge import create_app

# default to dev config because no one should use this in
# production anyway
env = os.environ.get('LOCAL_KNOWLEDGE_ENV', 'dev')
app = create_app('local_knowledge.settings.%sConfig' % env.capitalize())


#@app.before_first_request
#def settup_logging():
#    app.logger.add_handler(logging.StreamHandler())
