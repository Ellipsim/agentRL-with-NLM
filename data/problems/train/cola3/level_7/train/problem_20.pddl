

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b1)
(ontable b3)
(on b4 b3)
(on b5 b2)
(on b6 b7)
(ontable b7)
(on b8 b4)
(clear b5)
(clear b8)
)
(:goal
(and
(on b1 b6)
(on b4 b7)
(on b6 b4)
(on b7 b8))
)
)


