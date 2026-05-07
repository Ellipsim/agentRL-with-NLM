

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(ontable b1)
(on b2 b4)
(on b3 b2)
(on b4 b7)
(on b5 b3)
(on b6 b5)
(ontable b7)
(clear b1)
(clear b6)
)
(:goal
(and
(on b1 b7)
(on b4 b5)
(on b5 b6)
(on b6 b1))
)
)


