import { Canvas, useLoader } from "@react-three/fiber";
import { useRef, useState } from "react";
import { useDrag } from "@use-gesture/react";
import * as THREE from "three";
import robotPNG from "../assets/robot.png";

function RobotMesh({ lastMsg }) {
  const tex = useLoader(THREE.TextureLoader, robotPNG);
  const mesh = useRef();
  const [pos, setPos] = useState([0, 0, 0]);

  // kéo thả
  const bind = useDrag(({ offset: [x, y] }) =>
    setPos([x / 150, -y / 150, 0])
  );

  return (
    <mesh ref={mesh} position={pos} {...bind()}>
      <planeGeometry args={[3, 3]} />
      <meshBasicMaterial map={tex} transparent />
    </mesh>
  );
}

export default function Robot({ lastBotMsg }) {
  return (
    <>
      <Canvas camera={{ position: [0, 0, 5] }}>
        <ambientLight intensity={0.8} />
        <RobotMesh lastMsg={lastBotMsg} />
      </Canvas>
      {/* bubble */}
      {lastBotMsg && (
        <div className="absolute bottom-6 left-1/2 -translate-x-1/2 bg-white shadow-xl rounded-xl p-3 max-w-xs text-sm">
          {lastBotMsg.slice(0, 200)}…
        </div>
      )}
    </>
  );
}
