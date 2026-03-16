

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b8)
(on b3 b1)
(on b4 b5)
(ontable b5)
(on b6 b3)
(ontable b7)
(on b8 b4)
(clear b6)
(clear b7)
)
(:goal
(and
(on b2 b7)
(on b4 b1)
(on b5 b2)
(on b7 b8)
(on b8 b6))
)
)


