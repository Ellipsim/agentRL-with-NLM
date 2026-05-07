

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b8)
(on b3 b6)
(ontable b4)
(ontable b5)
(on b6 b2)
(on b7 b4)
(on b8 b1)
(clear b3)
(clear b7)
)
(:goal
(and
(on b2 b6)
(on b5 b2)
(on b6 b4)
(on b7 b3)
(on b8 b5))
)
)


