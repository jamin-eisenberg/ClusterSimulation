import {
    FormControl, FormHelperText, FormLabel,
    NumberDecrementStepper,
    NumberIncrementStepper,
    NumberInput,
    NumberInputField,
    NumberInputStepper
} from "@chakra-ui/react";
import {patchTo} from "../utils";

export function FormRequestNumberInput({title, help, url, min, max, step, value, setter}) {
    return (<FormControl>
        <FormLabel>{title}</FormLabel>
        <NumberInput allowMouseWheel value={value} min={min} max={max} step={step} onChange={(s, n) => {setter(s); patchTo(url, n);}}>
            <NumberInputField/>
            <NumberInputStepper>
                <NumberIncrementStepper/>
                <NumberDecrementStepper/>
            </NumberInputStepper>
        </NumberInput>
        <FormHelperText>{help}</FormHelperText>
    </FormControl>);
}
