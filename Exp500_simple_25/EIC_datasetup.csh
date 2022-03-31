#!/bin/tcsh

# Set up conda environment

conda activate /usr/local/usrapps/infews/group_env

# Submit multiple jobs at once

set folNameBase = Exp

foreach NN ( 500 )

	foreach UC ( _simple_ )

		foreach TC ( 25 )

			set dirName = ${folNameBase}${NN}${UC}${TC}
   			cd $dirName

			# Submit LSF job for the directory $dirName
   			bsub -n 8 -R "span[hosts=1]" -R "rusage[mem=5GB]" -W 5000 -o out.%J -e err.%J "python EICDataSetup.py"
			# Go back to upper level directory
    			cd ..

		end
	end
end

conda deactivate
