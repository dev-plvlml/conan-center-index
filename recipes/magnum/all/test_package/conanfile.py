from conans import ConanFile, CMake, tools
from conans.errors import ConanException
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "cmake_find_package"

    @property
    def _executables(self):
        available = []
        #            (executable, option name)
        all_execs = (("gl-info", "gl_info"), 
                     ("al-info", "al_info"), 
                     ("distancefieldconverter", "distance_field_converter"), 
                     ("fontconverter", "font_converter"), 
                     ("imageconverter", "image_converter"), 
                     ("sceneconverter", "scene_converter"))
        for executable, opt_name in all_execs:
            try:
                if getattr(self.options["magnum"], opt_name):
                    available.append(executable)
            except ConanException:
                pass
        return available

    def build(self):
        cmake = CMake(self)
        for exec in self._executables:
            cmake.definitions["EXEC_{}".format(exec.replace("-", "_")).upper()] = True
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self):
            for exec in self._executables:
                self.run("magnum-{} --help".format(exec), run_environment=True)

            bin_path = os.path.join("bin", "test_package")
            self.run(bin_path, run_environment=True)
