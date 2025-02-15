/*
 * Copyright (c) Contributors to the Open 3D Engine Project.
 * For complete copyright and license terms please see the LICENSE at the root of this distribution.
 *
 * SPDX-License-Identifier: Apache-2.0 OR MIT
 *
 */
#pragma once

#include <AzCore/Memory/SystemAllocator.h>
#include <Atom/RHI/RayTracingBufferPools.h>

namespace AZ
{
    namespace Null
    {
        class RayTracingBufferPools final
            : public RHI::RayTracingBufferPools
        {
        public:
            AZ_CLASS_ALLOCATOR(RayTracingBufferPools, AZ::SystemAllocator);

            static RHI::Ptr<RayTracingBufferPools> Create() { return aznew RayTracingBufferPools; }

        private:
            RayTracingBufferPools() = default;
        };
    }
}
