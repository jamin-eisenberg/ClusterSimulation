import './App.css';

import {
    Button,
    ChakraProvider, FormControl, FormHelperText, FormLabel
} from '@chakra-ui/react'
import {FormRequestNumberInput} from "./components/FormRequestNumberInput";
import {SketchPicker} from "react-color";
import {RequestNumberInput} from "./components/RequestNumberInput";
import {useEffect, useState} from "react";
import {getState, patchTo} from "./utils";

function App() {
    const base_url = 'http://raspberrypi.local/'
    // TODO only send color on finish picking?
    // TODO long test, with other computer client
    // TODO aesthetics

    const [color1, setColor1] = useState({hex: "#000000"});
    const [color2, setColor2] = useState({hex: "#000000"});
    const [color3, setColor3] = useState({hex: "#000000"});
    const [color4, setColor4] = useState({hex: "#000000"});

    const [particleRadius, setParticleRadius] = useState();
    const [particleInteractionRadius, setParticleInteractionRadius] = useState();
    const [particleCount, setParticleCount] = useState();
    const [frictionFactor, setFrictionFactor] = useState();
    const [disturbanceAmount, setDisturbanceAmount] = useState();
    const [disturbanceDerivative, setDisturbanceDerivative] = useState();
    const [distanceReadPeriod, setDistanceReadPeriod] = useState();

    const [colorInteractions, setColorInteractions] = useState([]);

    function colorInteractionsSetter(n) {
        return (val) => {
            setColorInteractions(colorInteractions.map((c, i) => {
                if (i === n) {
                    return val;
                } else {
                    return c;
                }
            }));
        }
    }

    function setRandomColorInteractions() {
        const newColorInteractions = colorInteractions.map(() => Math.floor(Math.random() * 400 - 200));
        setColorInteractions(newColorInteractions);
        newColorInteractions.map((c, n) => patchTo(base_url + `${Math.floor(n / 4)}/to/${n % 4}`, c))
    }

    useEffect(() => {
        const fetchState = async () => {
            let state = await getState(base_url);
            state = await state.json();

            setParticleRadius(state[0]);
            setParticleInteractionRadius(state[1]);
            setFrictionFactor(state[2]);
            setDisturbanceAmount(state[5]);
            setDisturbanceDerivative(state[6]);
            setDistanceReadPeriod(state[7]);
            setParticleCount(state[8]);

            setColor1({r: state[9], g: state[10], b: state[11]});
            setColor2({r: state[12], g: state[13], b: state[14]});
            setColor3({r: state[15], g: state[16], b: state[17]});
            setColor4({r: state[18], g: state[19], b: state[20]});

            setColorInteractions(state.slice(21));
        }

        fetchState();
    }, []);

    function handleColorChange(newColor, colorNum) {
        newColor = newColor.rgb;
        if (colorNum === 0) {
            setColor1(newColor)
        } else if (colorNum === 1) {
            setColor2(newColor)
        } else if (colorNum === 2) {
            setColor3(newColor)
        } else if (colorNum === 3) {
            setColor4(newColor)
        }
        patchTo(base_url + `color/${colorNum}/to/${newColor.r}/${newColor.g}/${newColor.b}`)
    }

    return (
        <ChakraProvider>
            <div className="App">
                <header className="App-header">
                    <FormRequestNumberInput value={particleRadius} setter={setParticleRadius} title={'Particle radius'} help={'How big the particle is in pixels.'}
                                            url={base_url + 'particle-radius'} min={0}/>
                    <FormRequestNumberInput value={particleInteractionRadius} setter={setParticleInteractionRadius} title={'Particle interaction radius'} help={'How far away a particle can be from another particle before they stop interacting.'}
                                            url={base_url + 'particle-interaction-radius'} min={0}/>
                    <FormRequestNumberInput value={particleCount} setter={setParticleCount} title={'Particle count'} help={'How many total particles there are.'}
                                            url={base_url + 'particle-count'} min={1}/>
                    <FormRequestNumberInput value={frictionFactor} setter={setFrictionFactor} title={'Friction factor'} help={"What portion of a particle's speed is maintained frame-to-frame."}
                                            url={base_url + 'friction-coefficient'} min={0} max={1} step={0.01}/>
                    <FormRequestNumberInput value={disturbanceAmount} setter={setDisturbanceAmount} title={'Disturbance amount'} help={"How much particles attract each other when someone walks in front of the ultrasonic sensor. Attraction is positive, repulsion is negative."}
                                            url={base_url + 'disturbance'} step={1}/>
                    <FormRequestNumberInput value={disturbanceDerivative} setter={setDisturbanceDerivative} title={'Disturbance derivative'} help={"How much the distance (in mm) the sensor senses has to change before causing a disturbance."}
                                            url={base_url + 'disturbance-derivative'} min={0} step={1}/>
                    <FormRequestNumberInput value={distanceReadPeriod} setter={setDistanceReadPeriod} title={'Distance read period'} help={"How long (in seconds) the distance sensor waits between reading distance."}
                                            url={base_url + 'distance-read-period'} min={0.05} step={0.1}/>
                    <FormControl>
                        <FormLabel>Color interactions</FormLabel>
                        <FormHelperText>(e.g. Row Color 1, Column Color 3 = -2 states that color 1 is repelled by color 3 with a strength of 2)</FormHelperText>
                        <table>
                            <tbody>
                                <tr>
                                    <td></td>
                                    <td><span style={{"color": `rgba(${color1.r}, ${color1.g}, ${color1.b}, 100)` }}>Color 1</span></td>
                                    <td><span style={{"color": `rgba(${color2.r}, ${color2.g}, ${color2.b}, 100)` }}>Color 2</span></td>
                                    <td><span style={{"color": `rgba(${color3.r}, ${color3.g}, ${color3.b}, 100)` }}>Color 3</span></td>
                                    <td><span style={{"color": `rgba(${color4.r}, ${color4.g}, ${color4.b}, 100)` }}>Color 4</span></td>
                                </tr>
                                <tr>
                                    <td><span style={{"color": `rgba(${color1.r}, ${color1.g}, ${color1.b}, 100)` }}>Color 1</span></td>
                                    <td><RequestNumberInput value={colorInteractions[0]} setter={colorInteractionsSetter(0)} url={base_url + '0/to/0'}/></td>
                                    <td><RequestNumberInput value={colorInteractions[1]} setter={colorInteractionsSetter(1)} url={base_url + '0/to/1'}/></td>
                                    <td><RequestNumberInput value={colorInteractions[2]} setter={colorInteractionsSetter(2)} url={base_url + '0/to/2'}/></td>
                                    <td><RequestNumberInput value={colorInteractions[3]} setter={colorInteractionsSetter(3)} url={base_url + '0/to/3'}/></td>
                                </tr>
                                <tr>
                                    <td><span style={{"color": `rgba(${color2.r}, ${color2.g}, ${color2.b}, 100)` }}>Color 2</span></td>
                                    <td><RequestNumberInput value={colorInteractions[4]} setter={colorInteractionsSetter(4)} url={base_url + '1/to/0'}/></td>
                                    <td><RequestNumberInput value={colorInteractions[5]} setter={colorInteractionsSetter(5)} url={base_url + '1/to/1'}/></td>
                                    <td><RequestNumberInput value={colorInteractions[6]} setter={colorInteractionsSetter(6)} url={base_url + '1/to/2'}/></td>
                                    <td><RequestNumberInput value={colorInteractions[7]} setter={colorInteractionsSetter(7)} url={base_url + '1/to/3'}/></td>
                                </tr>
                                <tr>
                                    <td><span style={{"color": `rgba(${color3.r}, ${color3.g}, ${color3.b}, 100)` }}>Color 3</span></td>
                                    <td><RequestNumberInput value={colorInteractions[8]} setter={colorInteractionsSetter(8)} url={base_url + '2/to/0'}/></td>
                                    <td><RequestNumberInput value={colorInteractions[9]} setter={colorInteractionsSetter(9)} url={base_url + '2/to/1'}/></td>
                                    <td><RequestNumberInput value={colorInteractions[10]} setter={colorInteractionsSetter(10)} url={base_url + '2/to/2'}/></td>
                                    <td><RequestNumberInput value={colorInteractions[11]} setter={colorInteractionsSetter(11)} url={base_url + '2/to/3'}/></td>
                                </tr>
                                <tr>
                                    <td><span style={{"color": `rgba(${color4.r}, ${color4.g}, ${color4.b}, 100)` }}>Color 4</span></td>
                                    <td><RequestNumberInput value={colorInteractions[12]} setter={colorInteractionsSetter(12)} url={base_url + '3/to/0'}/></td>
                                    <td><RequestNumberInput value={colorInteractions[13]} setter={colorInteractionsSetter(13)} url={base_url + '3/to/1'}/></td>
                                    <td><RequestNumberInput value={colorInteractions[14]} setter={colorInteractionsSetter(14)} url={base_url + '3/to/2'}/></td>
                                    <td><RequestNumberInput value={colorInteractions[15]} setter={colorInteractionsSetter(15)} url={base_url + '3/to/3'}/></td>
                                </tr>
                            </tbody>
                        </table>
                        <Button onClick={setRandomColorInteractions}>Random color interactions</Button>
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

export default App;
