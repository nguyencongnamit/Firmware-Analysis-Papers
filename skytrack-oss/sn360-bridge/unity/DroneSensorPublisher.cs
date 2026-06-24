// sn360-bridge — Unity sensor publisher.
//
// Attach to a drone GameObject. Each FixedUpdate it samples the body's pose and
// velocity and hands them to the transport (UDP to common/, or a ROS 2 client).
// This is the engine-side half of the bridge; the message encoding lives in
// common/. Kept dependency-light so it compiles in a stock Unity project.

using UnityEngine;

namespace Sn360.Bridge
{
    [RequireComponent(typeof(Rigidbody))]
    public class DroneSensorPublisher : MonoBehaviour
    {
        [Tooltip("How often to publish sensor frames (Hz).")]
        public float publishRateHz = 50f;

        [Tooltip("Bridge endpoint host:port for the common/ transport.")]
        public string endpoint = "127.0.0.1:14550";

        private Rigidbody _rb;
        private float _accum;
        private IBridgeTransport _transport;

        void Awake()
        {
            _rb = GetComponent<Rigidbody>();
            // Swap for a real UDP/ROS2 transport; LogTransport just prints frames.
            _transport = new LogTransport();
            _transport.Connect(endpoint);
        }

        void FixedUpdate()
        {
            _accum += Time.fixedDeltaTime;
            float period = 1f / Mathf.Max(1f, publishRateHz);
            if (_accum < period) return;
            _accum = 0f;

            // ENU: Unity is left-handed Y-up; convert to ENU (x=East, y=North, z=Up).
            Vector3 p = transform.position;
            Vector3 v = _rb.velocity;
            var frame = new SensorFrame
            {
                t = Time.timeAsDouble,
                px = p.x, py = p.z, pz = p.y,
                vx = v.x, vy = v.z, vz = v.y,
                roll = transform.eulerAngles.z * Mathf.Deg2Rad,
                pitch = transform.eulerAngles.x * Mathf.Deg2Rad,
                yaw = transform.eulerAngles.y * Mathf.Deg2Rad
            };
            _transport.PublishSensors(frame);
        }

        void OnDestroy() => _transport?.Dispose();
    }
}
