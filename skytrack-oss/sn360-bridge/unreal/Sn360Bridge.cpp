// sn360-bridge — Unreal Engine 5 plugin (implementation skeleton).

#include "Sn360Bridge.h"

USn360BridgeComponent::USn360BridgeComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void USn360BridgeComponent::BeginPlay()
{
    Super::BeginPlay();
    // TODO: connect transport (UDP to common/, or rclc ROS 2 client) using Endpoint.
    UE_LOG(LogTemp, Log, TEXT("[sn360-bridge] BeginPlay endpoint=%s"), *Endpoint);
}

void USn360BridgeComponent::TickComponent(float DeltaTime, ELevelTick TickType,
                                          FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

    Accumulator += DeltaTime;
    const float Period = 1.f / FMath::Max(1.f, PublishRateHz);
    if (Accumulator >= Period)
    {
        Accumulator = 0.f;
        PublishSensors();
    }
    ApplyPendingCommand();
}

void USn360BridgeComponent::PublishSensors()
{
    const AActor* Owner = GetOwner();
    if (!Owner) return;

    // UE5 is cm, X-forward/Y-right/Z-up, left-handed. Convert to ENU meters.
    const FVector P = Owner->GetActorLocation() / 100.f;
    const FVector V = Owner->GetVelocity() / 100.f;
    FSn360SensorFrame Frame;
    Frame.T = 0.0; // fill from world time
    Frame.PositionENU = FVector(P.X, P.Y, P.Z);
    Frame.VelocityENU = FVector(V.X, V.Y, V.Z);
    // TODO: transport->PublishSensors(Frame);
}

void USn360BridgeComponent::ApplyPendingCommand()
{
    // TODO: poll transport for the latest velocity setpoint and drive the body.
}
