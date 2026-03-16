

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b7)
(ontable b4)
(on b5 b8)
(on b6 b2)
(on b7 b4)
(on b8 b6)
(clear b3)
(clear b5)
)
(:goal
(and
(on b1 b6)
(on b2 b3)
(on b6 b4)
(on b7 b8))
)
)


