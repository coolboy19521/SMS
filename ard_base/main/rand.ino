#define ANALOG_INPUT   A0                       // defining analog input at A0

int    analog_output ;                                                       // This will read the analog value
int    revised_output;                                                      // variable to store the corrected value

float  temp_C ;                                                                  // Variable for storing the temperature
float  temp_f ;                                                                   // Variable for storing the fahrenheit

void setup ( )                                                                     // Anything written I it will run once.
{
  pinMode ( ANALOG_INPUT, INPUT )  ;                 // declaring A0 as input pin

  Serial.begin ( 9600 ) ;                                                     // selecting the baud rate at 9600
  Serial.println (" microcontrollerslab.com : The data is " ) ;
}

void loop ( )                                                                                        // Anything written in it will run continuously
{
  analog_output = analogRead ( ANALOG_INPUT ) ;         // Reading the analog value and storing in analog_output

  Serial.print ( " Analog value: " ) ;                                       
  Serial.print ( analog_output, DEC) ;                                    // This will display the analog value

   revised_output= map ( analog_output, 0, 1023, 1023, 0 ) ;

   temp_C    = Thermistor ( revised_output ) ;
  temp_f = ( temp_C * 9.0 ) / 5.0 + 32.0 ;


  Serial.print ( " Temperature: " ) ;
  Serial.print ( temp_f, 1 ) ;                                           // This will display the temperature in Fahrenheit
  Serial.print (" F  " ) ;

  Serial.print  (temp_C, 1 ) ;                                          // This will display the temperature in Celcius
  Serial.println (" C " ) ; 

  delay ( 10000 ) ;                                                                   // Wait for 1 second
}

double Thermistor ( int RawADC )
{
  double Temp ;
  

  Temp = log (10240000 / RawADC - 10000);
  Temp = 1 / ( 0.001129148 + ( 0.000234125 * Temp ) + ( 0.0000000876741 * Temp * Temp * Temp ) ) ;
  Temp = Temp - 273.15 ;            // This will Convert Kelvin to Celcius

  return Temp ;
}