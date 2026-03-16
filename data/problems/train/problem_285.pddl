

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b7)
(ontable b3)
(on b4 b5)
(on b5 b1)
(on b6 b2)
(ontable b7)
(clear b4)
(clear b6)
)
(:goal
(and
(on b2 b1)
(on b3 b7)
(on b5 b6)
(on b6 b3)
(on b7 b2))
)
)


