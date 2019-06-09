# Welcome to CHF Inspector!

Here's a list of relevant files as well as a simple step by step run-through of the entire process. The relevant results are stored in folders for organization.

# Items

**CHF_selection.xml:** Contains the state machine of the two protocols I modeled in xml form.

**ir2smv.py:** Script for converting xml file to smv file that can be ran through NuSMV. Taken directly from LTEInspector, located at https://github.com/relentless-warrior/LTEInspector/tree/master/model/MC

**properties.diff:** List of properties to add to the end of the smv file after it is generated.

**trace2dot.py:** Turns the output (traces) from NuSMV into a dot file, which can be converted into a visual state machine.

# Process

**Step 1:** Run the following command: `python ir2smv.py -i CHF_selection.xml -o chf.smv`

This will convert the state machine represented in the xml file and turn it into an smv file, which is the input type for NuSMV. 

**Step 1.5 OPTIONAL:** For visualizing the state machine only.

The above command will also generate a .dot file of the state machine.

To turn the .dot file into a visually friendly pdf, run this command: `dot -Tps [name of dot file].dot -o [name your own output].ps`

**Step 2:** Copy-paste the properties listed in properties.diff into the bottom of the smv file. This is necessary because the ir2smv script does not do this automatically. It must be done manually.

**Step 3:** Download whatever version of NuSMV you would like at http://nusmv.fbk.eu/NuSMV/download/getting-v2.html. Getting this to work is a little finicky, so the following instructions will be from my point of view.
NuSMV is installed in the root directory of my computer. From there, cd into the folder containing NuSMV. Then cd bin. There should be an executable called NuSMV in this file. Now copy the smv file that was generated above
INTO THE SAME FOLDER that this executable is located.

**Step 4:** There are two options that we known of to run NuSMV.

`./NuSMV [name of file].smv`

This is a basic run.

`./NuSMV -bmc -bmc_length [desired length] [name of file].smv`

This is a bounded model checker. In other words it will only run the model up to a certain number of steps, which is useful when there is an infinite loop in the state machine.
Without the -bmc_length [desired length] specified, the default length is 10.

**Step 5:** NuSMV should spit out a counterexample into the terminal. Copy this output and save it in a file. Or don't, because you're done at this point and can do whatever you want with the output.

**Step 5.5 OPTIONAL:** You're done once the counterexample is generated. However, for visualization purposes you can go back to the original directory with the counterexample in tow.
Once there, run `python3 trace2dot.py [name of the file containg counterexample]` to get a .dot file visually representing the counterexample. Use the same command as above to convert the .dot file into a visually friendly format.

Check out the counterexamples folder for example output of the counterexamples (text counterexamples and visualization both included)

Thanks for reading! :+1:
