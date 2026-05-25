# docker-images-homework

ROS / Gazebo / 커스텀 ROS 노드 이미지 3개를 `main` push 시 GitHub Actions가 자동으로 빌드해서 Docker Hub에 push.

| 이미지 | 내용 |
|---|---|
| `hsjin94/ros2-jazzy` | ROS 2 Jazzy desktop (Ubuntu 24.04) |
| `hsjin94/gazebo-harmonic` | Gazebo Harmonic (Ubuntu 24.04) |
| `hsjin94/marine-ctrl` | ROS 2 + `/cmd_vel` Twist publisher (auto / keyboard) |

```bash
docker pull hsjin94/marine-ctrl:latest
docker run --rm hsjin94/marine-ctrl:latest
```
