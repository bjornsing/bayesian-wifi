
import sys
import re
import pandas as pd

if len(sys.argv) <= 1:
	sys.stderr.write('Usage: python log2csv.py rates.csv\n')
	quit(1)

columns = ['mode', 'guard', 'streams', 'use',
           'name', 'idx', 'airtime', 'max_tp',
           'avg_tp', 'avg_prob', 'sd_prob',
           'last_prob', 'last_retry', 'last_suc', 'last_att',
           'sum_success', 'sum_attempts',
           'unknown_1', 'unknown_2', 'unknown_3']

rates = pd.read_csv(sys.argv[1], names=columns, index_col='idx')

print "time,mac,mode,streams,guard,name,airtime,ampdu_len,success"
for line in sys.stdin:
	# Example line:
	#  Mon Oct 24 19:30:46 2016 kern.debug kernel: [ 1682.439798] xmit: ec:08:6b:19:02:9b, 17, 1, 1, 1

	m = re.match("^[^\[]*\[\W*([0-9.]*)\] xmit: ([0-9a-f:]*), ([0-9]*), ([0-9]*), ([0-9]*), ([01])", line)

	if m:
		time      = m.group(1)
		mac       = m.group(2)
		idx       = int(m.group(3))
		count     = int(m.group(4))
		ampdu_len = m.group(5)
		success   = int(m.group(6))

		for xmit in range(1, count + 1):
			values = [time, mac, rates.ix[idx, 'mode'], rates.ix[idx, 'streams'], 
				  rates.ix[idx, 'guard'], rates.ix[idx, 'name'].lstrip().rstrip(),
				  rates.ix[idx, 'airtime'], ampdu_len, 0 if not success or xmit < count else 1]

			print ','.join([str(v) for v in values])

