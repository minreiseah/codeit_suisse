from flask import Flask
app = Flask(__name__)

import myapp.routes.square
import myapp.routes.tickerstream
import myapp.routes.cryptocollapz
import myapp.routes.rubiks
import myapp.routes.calendarDays
import myapp.routes.travelling
import myapp.routes.stig_full
import myapp.routes.stig_warmup
import myapp.routes.cauldrons
import myapp.routes.quordle