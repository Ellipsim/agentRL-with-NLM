

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b7)
(on b2 b3)
(ontable b3)
(on b4 b2)
(ontable b5)
(on b6 b1)
(on b7 b4)
(on b8 b6)
(clear b5)
(clear b8)
)
(:goal
(and
(on b2 b8)
(on b3 b6)
(on b4 b2)
(on b6 b7)
(on b7 b4)
(on b8 b1))
)
)


