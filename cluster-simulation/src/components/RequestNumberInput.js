import {
    NumberDecrementStepper,
    NumberIncrementStepper,
    NumberInput,
    NumberInputField,
    NumberInputStepper
} from "@chakra-ui/react";
import {patch_to} from "../utils";

export function RequestNumberInput({url, min, max, step}) {
    return (
        <NumberInput allowMouseWheel min={min} max={max} step={step} onChange={(_, n) => patch_to(url, n)}>
            <NumberInputField/>
            <NumberInputStepper>
                <NumberIncrementStepper/>
                <NumberDecrementStepper/>
            </NumberInputStepper>
        </NumberInput>);
}
