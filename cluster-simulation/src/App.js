import './App.css';

import {
    ChakraProvider, FormControl, FormHelperText, FormLabel
} from '@chakra-ui/react'
import {FormRequestNumberInput} from "./components/FormRequestNumberInput";
import {SketchPicker} from "react-color";
import {RequestNumberInput} from "./components/RequestNumberInput";
import {useState} from "react";
import {patch_to} from "./utils";

function App() {
    const base_url = 'http://192.168.0.3:5000/' // TODO change to raspi
    // TODO fetch current state at start

    const [color1, setColor1] = useState({hex: "#000000"});
    const [color2, setColor2] = useState({hex: "#000000"});
    const [color3, setColor3] = useState({hex: "#000000"});
    const [color4, setColor4] = useState({hex: "#000000"});

    function handleColorChange(newColor, colorNum) {
        if (colorNum === 0) {
            setColor1(newColor)
        } else if (colorNum === 1) {
            setColor2(newColor)
        } else if (colorNum === 2) {
            setColor3(newColor)
        } else if (colorNum === 3) {
            setColor4(newColor)
        }
        patch_to(base_url + `color/${colorNum}/to/${newColor.rgb.r}/${newColor.rgb.g}/${newColor.rgb.b}`)
    }

    return (
        <ChakraProvider>
            <div className="App">
                <header className="App-header">
                    <FormRequestNumberInput title={'Particle radius'} help={'How big the particle is in pixels.'}
                                            url={base_url + 'particle-radius'} min={0}/>
                    <FormRequestNumberInput title={'Particle interaction radius'} help={'How far away a particle can be from another particle before they stop interacting.'}
                                            url={base_url + 'particle-interaction-radius'} min={0}/>
                    <FormRequestNumberInput title={'Particle count'} help={'How many total particles there are.'}
                                            url={base_url + 'particle-count'} min={1}/>
                    <FormRequestNumberInput title={'Friction factor'} help={"What portion of a particle's speed is maintained frame-to-frame."}
                                            url={base_url + 'friction-coefficient'} min={0} max={1} step={0.01}/>
                    <FormRequestNumberInput title={'Disturbance amount'} help={"How much particles attract each other when someone walks in front of the ultrasonic sensor. Attraction is positive, repulsion is negative."}
                                            url={base_url + 'disturbance'} step={1}/>
                    <FormRequestNumberInput title={'Disturbance derivative'} help={"How much the distance (in mm) the sensor senses has to change before causing a disturbance."}
                                            url={base_url + 'disturbance-derivative'} min={0} step={1}/>
                    <FormRequestNumberInput title={'Distance read period'} help={"How long (in seconds) the distance sensor waits between reading distance."}
                                            url={base_url + 'distance-read-period'} min={0.05} step={0.1}/>
                    <FormControl>
                        <FormLabel>Color interactions</FormLabel>
                        <FormHelperText>(e.g. Row Color 1, Column Color 3 = -2 states that color 1 is repelled by color 3 with a strength of 2)</FormHelperText>
                        <table>
                            <tbody>
                                <tr>
                                    <td></td>
                                    <td><span style={{"color": color1.hex }}>Color 1</span></td>
                                    <td><span style={{"color": color2.hex }}>Color 2</span></td>
                                    <td><span style={{"color": color3.hex }}>Color 3</span></td>
                                    <td><span style={{"color": color4.hex }}>Color 4</span></td>
                                </tr>
                                <tr>
                                    <td><span style={{"color": color1.hex }}>Color 1</span></td>
                                    <td><RequestNumberInput url={base_url + '0/to/0'}/></td>
                                    <td><RequestNumberInput url={base_url + '0/to/1'}/></td>
                                    <td><RequestNumberInput url={base_url + '0/to/2'}/></td>
                                    <td><RequestNumberInput url={base_url + '0/to/3'}/></td>
                                </tr>
                                <tr>
                                    <td><span style={{"color": color2.hex }}>Color 2</span></td>
                                    <td><RequestNumberInput url={base_url + '1/to/0'}/></td>
                                    <td><RequestNumberInput url={base_url + '1/to/1'}/></td>
                                    <td><RequestNumberInput url={base_url + '1/to/2'}/></td>
                                    <td><RequestNumberInput url={base_url + '1/to/3'}/></td>
                                </tr>
                                <tr>
                                    <td><span style={{"color": color3.hex }}>Color 3</span></td>
                                    <td><RequestNumberInput url={base_url + '2/to/0'}/></td>
                                    <td><RequestNumberInput url={base_url + '2/to/1'}/></td>
                                    <td><RequestNumberInput url={base_url + '2/to/2'}/></td>
                                    <td><RequestNumberInput url={base_url + '2/to/3'}/></td>
                                </tr>
                                <tr>
                                    <td><span style={{"color": color4.hex }}>Color 4</span></td>
                                    <td><RequestNumberInput url={base_url + '3/to/0'}/></td>
                                    <td><RequestNumberInput url={base_url + '3/to/1'}/></td>
                                    <td><RequestNumberInput url={base_url + '3/to/2'}/></td>
                                    <td><RequestNumberInput url={base_url + '3/to/3'}/></td>
                                </tr>
                            </tbody>
                        </table>
                    </FormControl>
                    <FormControl>
                        <FormLabel>Colors</FormLabel>
                        <table>
                            <tbody>
                            <tr>
                                <td>Color 1</td>
                                <td>Color 2</td>
                                <td>Color 3</td>
                                <td>Color 4</td>
                            </tr>
                            <tr>
                                <td><SketchPicker color={color1} onChange={(color, _) => handleColorChange(color, 0)}/></td>
                                <td><SketchPicker color={color2} onChange={(color, _) => handleColorChange(color, 1)}/></td>
                                <td><SketchPicker color={color3} onChange={(color, _) => handleColorChange(color, 2)}/></td>
                                <td><SketchPicker color={color4} onChange={(color, _) => handleColorChange(color, 3)}/></td>
                            </tr>
                            </tbody>
                        </table>
                    </FormControl>
                </header>
            </div>
        </ChakraProvider>
    );
}

// TODO random button for color interactions

export default App;
