# Copyright (c) 2010-2012, GEM Foundation.
#
# NRML is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NRML is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with NRML.  If not, see <http://www.gnu.org/licenses/>.


"""Simple objects models to represent elements of NRML artifacts. These models
are intended to be produced by NRML XML parsers and consumed by NRMl XML
serializers.
"""


def _deep_eq(a, b):
    """Deep compare two objects for equality by traversing __dict__s.

    :returns:
        True if the two objects are deeply equal, otherwise false.
    """
    try:
        _do_deep_eq(a, b)
    except ValueError:
        return False
    return True


def _do_deep_eq(a, b):
    """Do the actual deep comparison. If two items up for comparison is not
    equal, a :exception:`ValueError` is raised (to :function:`_deep_eq`).
    """
    if getattr(a, '__dict__', None) is None:
        # 'primitive' values with no __dict__
        if hasattr(a, '__class__'):
            _ensure(a.__class__ == b.__class__)
        _ensure(a == b)
    else:  # there's a __dict__
        for key, value in a.__dict__.items():
            if hasattr(value, '__dict__'):
                if hasattr(value, '__class__'):
                    _ensure(value.__class__ == b.__dict__[key].__class__)
                _do_deep_eq(value, b.__dict__[key])
            else:
                if hasattr(value, '__class__'):
                    _ensure(value.__class__ == b.__dict__[key].__class__)
                _ensure(value == b.__dict__[key])


def _ensure(expr):
    """Better than `assert`, because `python -O` can't turn this off."""
    if not expr:
        raise ValueError()


class BaseModel(object):
    """Base class for NRML models."""

    def __eq__(self, other):
        return _deep_eq(self, other)


class SourceModel(BaseModel):
    """Simple container for source objects, plus metadata.

    :param str name:
        Name of the source model.
    :param sources:
        Iterable of seismic source objects (:class:`PointSource`,
        :class:`AreaSource`, :class:`SimpleFaultSource`,
        :class:`ComplexFaultSource`).
    """

    def __init__(self, name=None, sources=None):
        self.name = name
        self.sources = sources

    def __iter__(self):
        return self.sources

    def next(self):
        for src in self.sources:
            yield src


class PointSource(BaseModel):
    """Basic object representation of a Point Source.

    :param str id:
        Source identifier, unique within a given model.
    :param str name:
        Human-readable name for the source.
    :param str trt:
        Tectonic Region Type.
    :param geometry:
        :class:`PointGeometry` instance.
    :param str mag_scale_rel:
        Magnitude Scaling Relationship.
    :param float rupt_aspect_ratio:
        Rupture Aspect Ratio.
    :param mfd:
        Magnitude Frequency Distribution. An instance of
        :class:`IncrementalMFD` or :class:`TGRMFD`.
    :param list nodal_plane_dist:
        `list` of :class:`NodalPlane` objects which make up a Nodal Plane
        Distribution.
    :param list hypo_depth_dist:
        `list` of :class:`HypocentralDepth` instances which make up a
        Hypocentral Depth Distribution.
    """

    def __init__(self, id=None, name=None, trt=None, geometry=None,
                 mag_scale_rel=None, rupt_aspect_ratio=None, mfd=None,
                 nodal_plane_dist=None, hypo_depth_dist=None):
        self.id = id
        self.name = name
        self.trt = trt
        self.geometry = geometry
        self.mag_scale_rel = mag_scale_rel
        self.rupt_aspect_ratio = rupt_aspect_ratio
        self.mfd = mfd
        self.nodal_plane_dist = nodal_plane_dist
        self.hypo_depth_dist = hypo_depth_dist


class PointGeometry(BaseModel):
    """Basic object representation of a geometry for a :class:`PointSource`.

    :param str wkt:
        WKT representing the point geometry (a POINT).
    :param float upper_seismo_depth:
        Upper seismogenic depth.
    :param float lower_seismo_depth:
        Lower siesmogenic depth.
    """

    def __init__(self, wkt=None, upper_seismo_depth=None,
                 lower_seismo_depth=None):
        self.wkt = wkt
        self.upper_seismo_depth = upper_seismo_depth
        self.lower_seismo_depth = lower_seismo_depth


class AreaSource(PointSource):
    """Basic object representation of an Area Source.

    :param str id:
        Source identifier, unique within a given model.
    :param str name:
        Human-readable name for the source.
   :param str trt:
        Tectonic Region Type.
   :param geometry:
        :class:`AreaGeometry` instance.
    :param str mag_scale_rel:
        Magnitude Scaling Relationship.
    :param float rupt_aspect_ratio:
        Rupture Aspect Ratio.
    :param mfd:
        Magnitude Frequency Distribution. An instance of
        :class:`IncrementalMFD` or :class:`TGRMFD`.
    :param list nodal_plane_dist:
        `list` of :class:`NodalPlane` objects which make up a Nodal Plane
        Distribution.
    :param list hypo_depth_dist:
        `list` of :class:`HypocentralDepth` instances which make up a
        Hypocentral Depth Distribution.
    """


class AreaGeometry(PointGeometry):
    """Basic object representation of a geometry for a :class:`PointSource`.

    :param str wkt:
        WKT representing the area geometry (a POLYGON).
    :param float upper_seismo_depth:
        Upper seismogenic depth.
    :param float lower_seismo_depth:
        Lower siesmogenic depth.
    """


class SimpleFaultSource(BaseModel):
    """Basic object representation of a Simple Fault Source.

   :param str id:
        Source identifier, unique within a given model.
   :param str name:
        Human-readable name for the source.
   :param str trt:
        Tectonic Region Type.
   :param geometry:
        :class:`SimpleFaultGeometry` object.
    :param str mag_scale_rel:
        Magnitude Scaling Relationship.
    :param float rupt_aspect_ratio:
        Rupture Aspect Ratio.
    :param mfd:
        Magnitude Frequency Distribution. An instance of
        :class:`IncrementalMFD` or :class:`TGRMFD`.
    :param float rake:
        Rake angle.
    """

    def __init__(self, id=None, name=None, trt=None, geometry=None,
                 mag_scale_rel=None, rupt_aspect_ratio=None, mfd=None,
                 rake=None):
        self.id = id
        self.name = name
        self.trt = trt
        self.geometry = geometry
        self.mag_scale_rel = mag_scale_rel
        self.rupt_aspect_ratio = rupt_aspect_ratio
        self.mfd = mfd
        self.rake = rake


class SimpleFaultGeometry(BaseModel):
    """Basic object representation of a geometry for a
    :class:`SimpleFaultSource`.

   :param str wkt:
        WKT representing the fault trace of a simple fault (a LINESTRING).
    :param float upper_seismo_depth:
        Upper seismogenic depth.
    :param float lower_seismo_depth:
        Lower siesmogenic depth.
    """

    def __init__(self, id=None, name=None, wkt=None, dip=None,
                 upper_seismo_depth=None, lower_seismo_depth=None):
        self.wkt = wkt
        self.dip = dip
        self.upper_seismo_depth = upper_seismo_depth
        self.lower_seismo_depth = lower_seismo_depth


class ComplexFaultSource(SimpleFaultSource):
    """Basic object representation of a Complex Fault Source.

    :param str id:
        Source identifier, unique within a given model.
    :param str name:
        Human-readable name for the source.
   :param str trt:
        Tectonic Region Type.
    :param geometry:
        :class:`ComplexFaultGeometry` object.
    :param str mag_scale_rel:
        Magnitude Scaling Relationship.
    :param float rupt_aspect_ratio:
        Rupture Aspect Ratio.
    :param mfd:
        Magnitude Frequency Distribution. An instance of
        :class:`IncrementalMFD` or :class:`TGRMFD`.
    :param float rake:
        Rake angle.
    """


class ComplexFaultGeometry(BaseModel):
    """Basic object representation of a geometry for a
    :class:`ComplexFaultSource`.

    :param str top_edge_wkt:
        WKT representing the fault top edge (a LINESTRING).
    :param str bottom_edge_wkt:
        WKT representing the fault bottom edge (a LINESTRING).
    :param list int_edges:
        Intermediate fault edges, between the top edge and bottom edge.
        A `list` of `str` objects representing the WKT for each intermediate
        fault edge (each is a LINESTRING).

        This parameter is optional.
    """

    def __init__(self, top_edge_wkt=None, bottom_edge_wkt=None,
                 int_edges=None):
        self.top_edge_wkt = top_edge_wkt
        self.bottom_edge_wkt = bottom_edge_wkt
        self.int_edges = int_edges if int_edges is not None else []


class IncrementalMFD(BaseModel):
    """Basic object representation of an Incremental Magnitude Frequency
    Distribtion.

    :param float min_mag:
        The lowest possible magnitude for this MFD.
    :param float bin_width:
        Width of a single histogram bin.
    :param list occur_rates:
        `list` of occurrence rates (`float` values).
    """

    def __init__(self, min_mag=None, bin_width=None, occur_rates=None):
        self.min_mag = min_mag
        self.bin_width = bin_width
        self.occur_rates = occur_rates


class TGRMFD(BaseModel):
    """Basic object representation of a Truncated Gutenberg-Richter Magnitude
    Frequency Distribution.

    :param float a_val:
        10 ** a_val is the number of of earthquakes per year with magnitude
        greater than or equal to 0.
    :param float b_val:
        Decay rate of the exponential distribution.
    :param float min_mag:
        The lowest possible magnitude for this MFD.
    :param float max_mag:
        The highest possible magnitude for this MFD.
    """

    def __init__(self, a_val=None, b_val=None, min_mag=None, max_mag=None):
        self.a_val = a_val
        self.b_val = b_val
        self.min_mag = min_mag
        self.max_mag = max_mag


class NodalPlane(BaseModel):
    """Basic object representation of a single node in a Nodal Plane
    Distribution.

    :param float probability:
        Probability for this node in a Nodal Plane Distribution.
    :param float strike:
        Strike angle.
    :param float dip:
        Dip angle.
    :param float rake:
        Rake angle.
    """

    def __init__(self, probability=None, strike=None, dip=None, rake=None):
        self.probability = probability
        self.strike = strike
        self.dip = dip
        self.rake = rake