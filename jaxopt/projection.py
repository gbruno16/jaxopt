# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Projection operators."""

import jax
import jax.numpy as jnp


def projection_simplex(x: jnp.ndarray, s: float = 1.0) -> jnp.ndarray:
  """Projection onto the simplex.

  argmin_{p : 0 <= p <= s, jnp.sum(p) = s} ||x - p||

  Args:
    x: vector to project, an array of shape (n,).
    s: value p should sum to (default: 1.0).
  Returns:
    p: projected vector, an array of shape (n,).
  """
  n_features = x.shape[0]
  u = jnp.sort(x)[::-1]
  cssv = jnp.cumsum(u) - s
  ind = jnp.arange(n_features) + 1
  cond = u - cssv / ind > 0
  idx = jnp.count_nonzero(cond)
  threshold = cssv[idx - 1] / idx.astype(x.dtype)
  return jax.nn.relu(x - threshold)
