

(define (problem BW-rand-4)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b4)
(ontable b3)
(on b4 b3)
(clear b1)
)
(:goal
(and
(on b2 b4))
)
)


