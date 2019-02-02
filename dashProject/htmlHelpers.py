



def generateIndexString():
    index_string = '''
    <!DOCTYPE html>
    <html>
        <head>

            {%metas%}
            <title>Dive the Data</title>
            <link rel="icon" type="image/png" href="./assets/favicon/favicon-16.png" sizes="16x16">  
            <link rel="icon" type="image/png" href="./assets/favicon/favicon-32.png" sizes="32x32">  
            <link rel="icon" type="image/png" href="./assets/favicon/favicon-96.png" sizes="96x96"> 
            {%css%}

            <link rel="stylesheet" href="/assets/app.css">
        </head>
        <body>

            <div class="frame">
            {%app_entry%}


                <div id="about">

                    <div>

                        <div class="header">
                            <h1>A visualization for world flight routes data for different airlines.</h1>
                            <p>Fly the data was made by <a href="https://zoohair.github.io">Zouhair Mahboubi</a> 
                            as a submission to the <a href="https://www.thedataincubator.com">Data incubator</a>. The project is based on 
                            a previous visualization project <a href="https://www.divethedata.com">Dive the Data</a> for Marine Megafauna</p>
                        </div>

                        <div class="visualized">
                            <h2>What is Visualized Above?</h2>
                            <p>The route data is visualized using Plotly and Dash. 
                            The three Plotly graphs are cross graphs, meaning what you select in one graph is reflected in the other two.
                            A route map gives an overview of the origin/destination pairs. Using clustering algorithm, it is possible to get a 
                            better sense for the major traffic between the hubs<br>
                            An airlines graph gives an overview of the major airlines, and a breakdown of their passenger capacity.
                            A range graph shows a distribution of the length of flights, broken down by aircraft type.</p>
                        </div>

                        <div class="twocol">

                            <div class="collected">
                                <h2>How the data is collected?</h2>
                                <p>The routes and airport data was obtained from <a href="https://openflights.org/data.html">OpenFlights</a>. 
                                Unfortunately, the route data is a bit data. Aircraft performance was scrubbed 
                                from the <a href="https://contentzone.eurocontrol.int/apm/">Eurocontrol database</a>. </p>
                            </div>

                            <div class="contribute">
                                <h2>How can I contribute?</h2>
                                <p>If you have ideas on how to improve how the data is visualized, or more up to date 
                                routes data, please email me at <a href="mailto:zoohair@gmail.com">zoohair@gmail.com</a></p>
                            </div>

                        </div>

                    </div>

                </div>


                <div class="howto" id="howto">
                    <div class="intro">
                        <h2>How to use Plotly graphs</h2>
                        <p>Fly the data is built using interactive plotly graphs. 
                        This allows you to select and view the data you are most interested in.
                        Use the zoom/pans/select tools to explore the data.</p>
                    </div>

                </div> <!-- end of how to -->

            </div><!-- end frame -->


            <div id="footer">

                <p>© Fly The Data 2018</p>

            </div>

            <footer>
                {%config%}
                {%scripts%}
            </footer>
        </body>

    </html>
    '''

    return index_string