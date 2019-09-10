import numpy as np

__all__ = ['handlers']


def addmm(node):
    # [n, p] = aten::addmm([n(, p)], [n, m], [m, p], *, *)
    n, p = node.outputs[0].shape
    n, m = node.inputs[1].shape
    return n * m * p


def addmv(node):
    # [n] = aten::addmv([n], [n, m], [m], *, *)
    n, m = node.outputs[1].shape
    return n * m


def bmm(node):
    # [b, n, p] = aten::bmm([b, n, m], [b, m, p])
    b, n, p = node.outputs[0].shape
    b, n, m = node.inputs[0].shape
    return b * n * m * p


def matmul(node):
    return np.prod(node.inputs[0].shape + [node.inputs[1].shape[-1]])


def mul(node):
    os = node.outputs[0].shape
    return np.prod(os)


def convolution(node):
    os = node.outputs[0].shape
    ic = node.inputs[1].shape[1]
    ks = node.inputs[1].shape[2:]
    return np.prod(os) * ic * np.prod(ks)


def batch_norm(node):
    # `batch_norm` can be fused into its previous `linear` or `conv` layer
    # TODO: we should provide an option to not fuse `batch_norm` layer
    return 0


def layer_norm(node):
    os = node.outputs[0].shape
    return np.prod(os)


def mean(node):
    return 1


def avg_pool(node):
    os = node.outputs[0].shape
    return np.prod(os)


handlers = (
    ('aten::addmm', addmm),
    ('aten::addmv', addmv),
    ('aten::bmm', bmm),
    ('aten::matmul', matmul),
    (('aten::mul', 'aten::mul_'), mul),
    ('aten::_convolution', convolution),
    ('aten::batch_norm', batch_norm),
    ('aten::layer_norm', layer_norm),
    ('aten::mean', mean),

    (('aten::adaptive_avg_pool1d', 'aten::adaptive_avg_pool2d', 'aten::adaptive_avg_pool3d', 'aten::avg_pool1d',
      'aten::avg_pool2d', 'aten::avg_pool3d'), avg_pool),

    (('aten::adaptive_max_pool1d', 'aten::adaptive_max_pool2d', 'aten::adaptive_max_pool3d', 'aten::add', 'aten::add_',
      'aten::cat', 'aten::chunk', 'aten::clone', 'aten::contiguous', 'aten::div', 'aten::div_', 'aten::dropout',
      'aten::dropout_', 'aten::eq', 'aten::flatten', 'aten::hardtanh_', 'aten::int', 'aten::max_pool1d',
      'aten::max_pool2d', 'aten::max_pool3d', 'aten::ne', 'aten::relu', 'aten::relu_', 'aten::select', 'aten::size',
      'aten::slice', 'aten::softmax', 'aten::sum', 'aten::t', 'aten::transpose', 'aten::view', 'prim::constant',
      'prim::listconstruct', 'prim::listunpack', 'prim::numtotensor'), None)
)
