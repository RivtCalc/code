oncepy
======

The program **oncepy** takes a **on-c-e** ASCII model as input    
and returns a formatted structural engineering calculation. The    
program formats structural calculations using a simple, natural    
markup language.    

The beta code and documentation are released to solicit    
participation and feedback on basic concepts.  Currently the    
program can run usable calculation models, as illustrated in the    
examples. Some classes and methods are not implemented yet.    
The current beta development cycle will complete model operations,    
add input error checking, add a unit test framework and    
package the program for pypi distribution.    

Progress can be tracked at Trello:    
https://on-c-e.info    

Source code and documentation are here:    
    http://on-c-e.github.io/    

For further details refer to the user manual and programs here:    
    http://on-c-e.org/programs/    

email contact:    
r holland    
once.pyproject@gmail.com    

Running the Program    
===================    

Copy the **oncepy** package (folder) to the python/lib/site-packages    
directory. From a terminal window type:    

.. code:: python    

    python -m oncepy xxyy.model.txt (-c or -b)    


where *xxyy.model.txt* is the file name, xx is the chapter number    
and yy is the model number.    

The program will write the calc file calxxyy.model.txt and the    
-c or -b options will echo the calc to a console (-c) or    
a Windows browser (-b). The -b option is needed on Windows because    
of UTF-8 encoding limitations in the console.    

To open a terminal window in a folder in Windows 7 or 8 ,    
navigate to the folder using Explorer, hold the shift key,right click,    
click on 'open command window here' in the context menu.    

Change the browser encoding settings if needed:    
-----------------------------------------------    
Chrome  - type chrome:settings/fonts  in url bar -    
scroll to the bottom of the dialog box and make the change    

Firefox - options - content - advanced - UTF-8    

Internet Explorer - right click - encoding - UTF-8    

The program will execute the file and return results in files.    

To obtain a more complete UTF-8 font set install **DejaVu Mono** fonts    
http://dejavu-fonts.org/wiki/Main_Page    

    **methods:**    
        gen_paths()  find model and project paths    
        cmdline()  command line prompt    
        gen_files() generate new file names    
        out_term() check console printing flags    
        sum_calc() write calculation summary to stdout    
