// sn360-bridge — Unity command subscriber + transport interface.
//
// Receives velocity setpoints from the bridge and applies them to the Rigidbody.
// Defines the IBridgeTransport seam so the transport (UDP/ROS 2) can be swapped
// without touching the publisher/subscriber.

using System;
using UnityEngine;

namespace Sn360.Bridge
{
    [Serializable]
    public struct SensorFrame
    {
        public double t;
        public float px, py, pz;   // ENU position (m)
        public float vx, vy, vz;   // ENU velocity (m/s)
        public float roll, pitch, yaw; // rad
    }

    [Serializable]
    public struct CommandFrame
    {
        public float vx, vy, vz;   // ENU velocity setpoint (m/s)
    }

    public interface IBridgeTransport : IDisposable
    {
        void Connect(string endpoint);
        void PublishSensors(SensorFrame frame);
        bool TryGetCommand(out CommandFrame cmd);
    }

    /// <summary>No-network transport that logs frames — useful for first bring-up.</summary>
    public class LogTransport : IBridgeTransport
    {
        public void Connect(string endpoint) => Debug.Log($"[sn360-bridge] connect {endpoint}");
        public void PublishSensors(SensorFrame f) =>
            Debug.Log($"[sn360-bridge] pos=({f.px:F1},{f.py:F1},{f.pz:F1})");
        public bool TryGetCommand(out CommandFrame cmd) { cmd = default; return false; }
        public void Dispose() { }
    }

    [RequireComponent(typeof(Rigidbody))]
    public class MotorSubscriber : MonoBehaviour
    {
        private Rigidbody _rb;
        private IBridgeTransport _transport;

        void Awake()
        {
            _rb = GetComponent<Rigidbody>();
            _transport = new LogTransport();
            _transport.Connect("127.0.0.1:14550");
        }

        void FixedUpdate()
        {
            if (_transport.TryGetCommand(out var cmd))
            {
                // ENU setpoint -> Unity (Y-up) velocity.
                _rb.velocity = new Vector3(cmd.vx, cmd.vz, cmd.vy);
            }
        }

        void OnDestroy() => _transport?.Dispose();
    }
}
