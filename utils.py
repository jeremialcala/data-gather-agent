# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta,time



def get_timestamp(component='CORE'):
	return datetime.fromtimestamp(time.time()).strftime('[%Y.%m.%d %H:%M:%S.%f')[:-3] + '][' + component + ']'