

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b1)
(ontable b3)
(ontable b4)
(on b5 b7)
(on b6 b4)
(on b7 b8)
(on b8 b2)
(clear b3)
(clear b5)
)
(:goal
(and
(on b2 b8)
(on b4 b1)
(on b7 b4)
(on b8 b5))
)
)


