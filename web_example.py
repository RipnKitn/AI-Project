if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $conn = new mysqli($servername, $username, $password, $dbname); 

  $data = json_decode(file_get_contents('php://input'), true);
  //extract data out of JSON
  $symbol = $data['symbol'];
  $instrument = $data['instrument'];
  $tv_id = $data['tv_id'];
  $price = $data['price'];
  $execute = $data['execute'];
  $type_of_execute = $data['type_of_execute'];
  $strike_steps = $data['strike_steps'];
  $long_short = $data['long_short'];
  $amount = $data['amount'];
  $pl_start = $data['pl_start'];
  $sl_start = $data['sl_start'];
  $trailing_sl_percent = $data['trailing_sl_percent'];

  //Insert into DB
  $stmt = $conn->prepare("INSERT INTO alerts (symbol, instrument, tv_id, price, execute,     
                          type_of_execute, strike_steps, long_short, amount, pl_start, sl_start,
                          trailing_sl_percent) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
  $stmt->bind_param("sssdssisiddd", $symbol, $instrument, $tv_id, $price, $execute,         
                    $type_of_execute, $strike_steps, $long_short, $amount,
                    $pl_start, $sl_start, $trailing_sl_percent);
  $stmt->execute()
  $stmt->close();
  $conn->close();
}else {
    echo "Err";
}