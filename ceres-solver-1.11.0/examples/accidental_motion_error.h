// Ceres Solver - A fast non-linear least squares minimizer
// Copyright 2015 Google Inc. All rights reserved.
// http://ceres-solver.org/
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
// * Redistributions of source code must retain the above copyright notice,
//   this list of conditions and the following disclaimer.
// * Redistributions in binary form must reproduce the above copyright notice,
//   this list of conditions and the following disclaimer in the documentation
//   and/or other materials provided with the distribution.
// * Neither the name of Google Inc. nor the names of its contributors may be
//   used to endorse or promote products derived from this software without
//   specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.
//
// Author: sameeragarwal@google.com (Sameer Agarwal)
//
// Templated struct implementing the camera model and residual
// computation for bundle adjustment used by Noah Snavely's Bundler
// SfM system. This is also the camera model/residual for the bundle
// adjustment problems in the BAL dataset. It is templated so that we
// can use Ceres's automatic differentiation to compute analytic
// jacobians.
//
// For details see: http://phototour.cs.washington.edu/bundler/
// and http://grail.cs.washington.edu/projects/bal/

#ifndef CERES_EXAMPLES_ACCIDENTAL_MOTION_ERROR_H_
#define CERES_EXAMPLES_ACCIDENTAL_MOTION_ERROR_H_

#include "ceres/rotation.h"

namespace ceres {
namespace examples {

// Templated pinhole camera model for used with Ceres.  The camera is
// parameterized using 9 parameters: 3 for rotation, 3 for translation, 1 for
// focal length and 2 for radial distortion. The principal point is not modeled
// (i.e. it is assumed be located at the image center).
struct AccidentalMotionError {
  AccidentalMotionError(double observed_x, double observed_y)
      : observed_x(observed_x), observed_y(observed_y) {}

  template <typename T>
  bool operator()(const T* const camera,
                  const T* const point,
                  T* residuals) const {
    
    // camera[3,4,5] are the translation.
    T trans[3] = { camera[3], camera[4], camera[5] };

    // camera[0,1,2] are the rotation.
    T rot[3] = { camera[0], camera[1], camera[2] };

    // camera[6] is the focal length of the camera
    // const T& focal = camera[6];
    // focal length is set to be constant for now
    const T& focal = T(2720.0);

    // Compute point location
    T p[3] = { 
      point[0] / point[2], 
      point[1] / point[2], 
      T(1) / point[2] 
    };

    T image_x = T(observed_x) / focal;
    T image_y = T(observed_y) / focal;
    
    T ax = p[0] - rot[2] * p[1] + rot[1];
    T ay = p[1] - rot[0] + rot[2] * p[0];
    T c = -rot[1] * p[0] + rot[0] * p[1] + T(1);
    T ex = image_x * c - ax;
    T fx = image_x * trans[2] - trans[0];
    T ey = image_y * c - ay;
    T fy = image_y * trans[2] - trans[1];

    residuals[0] = T((ex + fx * p[2]) / (c + trans[2] * p[2]));
    residuals[1] = T((ey + fy * p[2]) / (c + trans[2] * p[2]));
    
    return true;
  }

  // Factory to hide the construction of the CostFunction object from
  // the client code.
  static ceres::CostFunction* Create(const double observed_x,
                                     const double observed_y) {
    return (new ceres::AutoDiffCostFunction<AccidentalMotionError, 2, 9, 3>(
                new AccidentalMotionError(observed_x, observed_y)));
  }

  double observed_x;
  double observed_y;
};


}  // namespace examples
}  // namespace ceres

#endif  // CERES_EXAMPLES_ACCIDENTAL_MOTION_ERROR_H_
