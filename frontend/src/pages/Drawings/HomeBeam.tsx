import React, { useRef, useEffect } from "react";
import { Canvas } from "react-three-fiber";

function Beam({ length, numDividers }: { length: number; numDividers: number}) {
    const canvasRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        // @ts-ignore
        const ctx = canvas.getContext("2d");

        // calculate the width of each divider
        const dividerWidth = length / numDividers;

        // set the starting x-coordinate
        let x = 0;

        // loop through each divider and draw a rectangle
        for (let i = 0; i < numDividers; i++) {
            ctx.fillStyle = "blue";
            ctx.fillRect(x, 10, dividerWidth, 50);

            // draw a rectangle at each end of the divider
            for (let j = 0; j < 2; j++) {
                ctx.fillStyle = "red";
                ctx.fillRect(x + (j * dividerWidth) - 5, 0, 10, 10);
                ctx.fillRect(x + (j * dividerWidth) - 5, 60, 10, 10);
            }

            x += dividerWidth;
        }
    }, [length, numDividers]);

    return (
        <div>
            <canvas ref={canvasRef} width={length} height={70} />
        </div>
    );
}

export default Beam;




