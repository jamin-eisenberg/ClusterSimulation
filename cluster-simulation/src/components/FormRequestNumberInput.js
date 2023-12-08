import {
    FormControl, FormHelperText, FormLabel,
    NumberDecrementStepper,
    NumberIncrementStepper,
    NumberInput,
    NumberInputField,
    NumberInputStepper
} from "@chakra-ui/react";
import {patch_to} from "../utils";

export function FormRequestNumberInput({title, help, url, min, max, step}) {
    return (<FormControl>
        <FormLabel>{title}</FormLabel>
        <NumberInput allowMouseWheel min={min} max={max} step={step} onChange={(_, n) => patch_to(url, n)}>
            <NumberInputField/>
            <NumberInputStepper>
                <NumberIncrementStepper/>
                <NumberDecrementStepper/>
            </NumberInputStepper>
        </NumberInput>
        <FormHelperText>{help}</FormHelperText>
    </FormControl>);
}
