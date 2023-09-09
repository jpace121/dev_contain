#
# Copyright 2023 James Pace
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Print some stuff I need to run on the host which I never remember.

def hints():
    x_host_text = "Run `xhost +` to disable x access control."

    total_text = "\n\t{}\n".format(x_host_text)

    print(total_text)

if __name__ == '__main__':
    hints()
