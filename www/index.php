<!DOCTYPE html>
<html class="no-js">
    <head>
        <meta charset="utf-8">
        <title>PVM - PhotoVoltaic Monitor</title>
        <meta name="description" content="PhotoVoltaic Monitor">
        <meta name="viewport" content="width=device-width">

        <link rel="stylesheet" href="css/bootstrap.min.css">
        <style>
            body {
                padding-top: 50px;
                padding-bottom: 20px;
            }
        </style>
        <link rel="stylesheet" href="css/bootstrap-theme.min.css">
        <link rel="stylesheet" href="css/main.css">

        <script src="js/vendor/modernizr-2.6.2-respond-1.1.0.min.js"></script>
    </head>
    <body>
    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href=".">PVM - PhotoVoltaic Monitor</a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <!--<li class="active"><a href="#">Home</a></li>-->
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown">Actions <b class="caret"></b></a>
              <ul class="dropdown-menu">
                <li><a href="realtime.php">Real time monitoring</a></li>
                <li><a href="#">Daily report</a></li>
                <li><a href="#">Monthly report</a></li>
                <li><a href="#">Yearly report</a></li>
                <li class="divider"></li>
                <!--<li class="dropdown-header">Nav header</li>-->
                <li><a href="#">Configuration</a></li>
                <li><a href="#">Log</a></li>
              </ul>
            </li>
            <li><a href="#about">About</a></li>
          </ul>
        </div><!--/.navbar-collapse -->
      </div>
    </div>

    <div class="container">
      <!-- Example row of columns -->
          <h2>Real time monitoring</h2>
	  <p><iframe seamless width="1800" height="1000" style="border: 0;" src="rt.php"></iframe></p>
      <hr>

      <!--
      <footer>
        <p>&copy; Company 2013</p>
      </footer>
      -->

    </div> <!-- /container -->        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
        <script>window.jQuery || document.write('<script src="js/vendor/jquery-1.10.1.min.js"><\/script>')</script>

        <script src="js/vendor/bootstrap.min.js"></script>

        <script src="js/main.js"></script>
    </body>
</html>
