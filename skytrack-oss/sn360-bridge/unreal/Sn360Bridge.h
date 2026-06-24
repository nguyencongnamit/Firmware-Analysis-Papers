// sn360-bridge — Unreal Engine 5 plugin (header).
//
// USceneComponent that mirrors the Unity publisher/subscriber: samples the
// owning actor's transform/velocity, publishes sensor frames, and applies
// incoming velocity setpoints. Transport lives behind ISn360Transport so UDP /
// ROS 2 can be swapped without touching gameplay code.

#pragma once

#include "CoreMinimal.h"
#include "Components/SceneComponent.h"
#include "Sn360Bridge.generated.h"

USTRUCT()
struct FSn360SensorFrame
{
    GENERATED_BODY()

    double T = 0.0;
    FVector PositionENU = FVector::ZeroVector; // x=East, y=North, z=Up (m)
    FVector VelocityENU = FVector::ZeroVector;
    FVector AttitudeRad = FVector::ZeroVector; // roll, pitch, yaw
};

UCLASS(ClassGroup = (Sn360), meta = (BlueprintSpawnableComponent))
class SN360BRIDGE_API USn360BridgeComponent : public USceneComponent
{
    GENERATED_BODY()

public:
    USn360BridgeComponent();

    UPROPERTY(EditAnywhere, Category = "sn360-bridge")
    float PublishRateHz = 50.f;

    UPROPERTY(EditAnywhere, Category = "sn360-bridge")
    FString Endpoint = TEXT("127.0.0.1:14550");

    virtual void TickComponent(float DeltaTime, ELevelTick TickType,
                               FActorComponentTickFunction* ThisTickFunction) override;

protected:
    virtual void BeginPlay() override;

private:
    float Accumulator = 0.f;
    void PublishSensors();
    void ApplyPendingCommand();
};
