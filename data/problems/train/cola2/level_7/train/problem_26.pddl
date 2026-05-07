

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(ontable b1)
(on b2 b5)
(ontable b3)
(on b4 b3)
(on b5 b1)
(on b6 b4)
(on b7 b2)
(on b8 b7)
(clear b6)
(clear b8)
)
(:goal
(and
(on b1 b3)
(on b2 b6)
(on b3 b4)
(on b4 b2)
(on b5 b1)
(on b6 b8))
)
)


