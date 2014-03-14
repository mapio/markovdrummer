from os.path import basename, splitext

def filebaseext( path ):
	return ( path, ) + splitext( basename( path ) )
