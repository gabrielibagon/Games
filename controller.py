
import open_bci_v3 as bci

board = bci.OpenBCIBoard()

	if not board.streaming:
		print("Error")
	else:
		def __call__(self,sample):
			sample = board.sample
			if sample:
				sample_string = "ID: %f\n%s\n%s" %(sample.id, str(sample.channel_data)[1:-1])
				print "---------------------------------"
				print sample_string
				print "---------------------------------"

