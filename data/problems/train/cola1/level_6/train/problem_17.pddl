

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b7)
(on b3 b1)
(ontable b4)
(on b5 b2)
(on b6 b5)
(on b7 b3)
(ontable b8)
(clear b4)
(clear b6)
)
(:goal
(and
(on b3 b4)
(on b4 b5)
(on b6 b2)
(on b8 b3))
)
)


