#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def get(event, context): 
    response = {
        'statusCode': 200,
        'body': json.dumps([{ 'id':'00001', 'name':'tanaka' }, { 'id':'00002', 'name':'hayashi' }])
    }
    return response