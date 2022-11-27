<!DOCTYPE html>
<html class="no-js">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="cache-control" content="no-cache">
        <meta http-equiv="pragma" content="no-cache">
        <meta http-equiv="expires" content="0">
        <meta http-equiv="refresh" content="10">
        <link rel="stylesheet" href="css/bootstrap.min.css">
        <link rel="stylesheet" href="css/bootstrap-theme.min.css">
        <link rel="stylesheet" href="css/main.css">
    </head>

<body>
<?php

$data_dir=getenv("data_dir");
$file=fopen($data_dir.'/pvm-rt.out','r');
if ($line=fgets($file)) {

   $st['0']='Inverter has just switched on';
   $st['1']='Waiting to start';
   $st['2']='Waiting to switch off';
   $st['3']='Constant volt. control';
   $st['4']='Feed-in mode';
   $st['8']='Self test';
   $st['9']='Test mode';
   $st['11']='Power limitation';
   $st['60']='PV voltage too high for feed-in';
   $st['61']='Power Control';
   $st['62']='Standalone mode';
   $st['63']='P(f) frequency-dependent power reduction';
   $st['64']='Output current limiting';

   $st['10']='Temperature inside high in unit';
   $st['18']='Error current switch-off';
   $st['19']='Generator insulation fault';
   $st['30']='Error measurement';
   $st['31']='RCD module error';
   $st['32']='Fault self test';
   $st['33']='Fault DC feed-in';
   $st['34']='Fault communication';
   $st['35']='Protection shutdown (SW)';
   $st['36']='Protection shutdown (HW)';
   $st['38']='Fault PV overvoltage';
   $st['41']='Line failure undervoltage L1';
   $st['42']='Line failure overvoltage L1';
   $st['43']='Line failure undervoltage L2';
   $st['44']='Line failure overvoltage L2';
   $st['45']='Line failure undervoltage L3';
   $st['46']='Line failure overvoltage L3';
   $st['47']='Line failure line-to-line voltage';
   $st['48']='Line failure: underfreq.';
   $st['49']='Line failure: overfreq.';
   $st['50']='Line failure average voltage';
   $st['57']='Waiting reconnect';
   $st['58']='Overtemperature control board ';
   $st['59']='Self test error';

   parse_str($line, $out);

   $d=date_parse_from_format('Y-m-d H:i:s', $out["timestamp"]);
   $year=sprintf('%\'04d',$d['year']);
   $day=sprintf('%\'02d',$d['day']);
   $month=sprintf('%\'02d',$d['month']);
   $hour=sprintf('%\'02d',$d['hour']);
   $minute=sprintf('%\'02d',$d['minute']);
   $second=sprintf('%\'02d',$d['second']);

   echo '<p><b>Date: '.$day.'/'.$month.'/'.$year.' '.$hour.':'.$minute.':'.$second.'</b> &ndash; ';
   echo '<b>Status: '.$out["status"].' - '.$st[$out["status"]].'</b> &ndash; ';
   echo '<b>Device temperature: '.$out["device_temperature"].' &deg;C</b></p>';
   echo '<table border="0">';
   echo '<tr>';
   echo '<td align="center"><img src="img/solar-panel.png" width="120" alt="panel"></td>';
   echo '<td width="10">&nbsp;</td>';
   echo '<td><p><b>Generator voltage: '.$out["generator_voltage"].' V</b><br>';
   echo '<b>Generator current: '.$out["generator_current"].' A</b><br>';
   echo '<b>Generator power: '.$out["generator_power"].' W</b></p></td>';
   $ddimg=$year.'/'.$month.'/pvm-'.$year.'-'.$month.'-'.$day.'-daily_details.png';
   $msimg=$year.'/'.$month.'/pvm-'.$year.'-'.$month.'-monthly_stats.png';
   $ysimg=$year.'/pvm-'.$year.'-yearly_stats.png';
   echo '<td rowspan="3">';
   echo '<a target="_top" href="output/'.$ddimg.'"><img src="output/'.$ddimg.'" alt="Daily graph" height="300"></a><br>';
   echo '<a target="_top" href="output/'.$msimg.'"><img src="output/'.$msimg.'" alt="Monthly stats" height="300"></a>';
   echo '</td>';
   echo '</tr>';
   echo '<tr>';
   echo '<td align="center"><img src="img/electric.png" alt="panel"><br></td>';
   echo '<td width="10">&nbsp;</td>';
   echo '<td><p><b>Grid voltage: '.$out["grid_voltage"].' V</b><br>';
   echo '<b>Grid current: '.$out["grid_current"].' A</b></p></td>';
   echo '</tr>';
   echo '<tr>';
   echo '<td align="center"><img src="img/electric-tower.png" width="120" alt="panel"><br></td>';
   echo '<td width="10">&nbsp;</td>';
   echo '<td><p><b>Delivered power: '.$out["delivered_power"].' W</b><br>';
   echo '<b>Daily yeld: '.$out["daily_yeld"].' W</b></p></td>';
   echo '</tr>';
   echo '<tr>';
   echo '<td colspan="3">';
   echo '<td><a target="_top" href="output/'.$ysimg.'"><img src="output/'.$ysimg.'" alt="Yearly stats" height="300"></a></td>';
   echo '</tr>';
   echo '</table>';
}

fclose($file);
?>
</body>
</html>
