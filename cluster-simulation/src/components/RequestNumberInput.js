import {
    NumberDecrementStepper,
    NumberIncrementStepper,
    NumberInput,
    NumberInputField,
    NumberInputStepper
} from "@chakra-ui/react";
import {patchTo} from "../utils";

export function RequestNumberInput({value, setter, url, min, max, step}) {
    return (
        <NumberInput allowMouseWheel value={value} min={min} max={max} step={step} onChange={(_, n) => {setter(n); patchTo(url, n);}}>
            <NumberInputField/>
            <NumberInputStepper>
                <NumberIncrementStepper/>
                <NumberDecrementStepper/>
            </NumberInputStepper>
        </NumberInput>);
}
