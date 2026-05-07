

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(ontable b1)
(on b2 b6)
(ontable b3)
(on b4 b7)
(on b5 b4)
(on b6 b1)
(on b7 b3)
(clear b2)
(clear b5)
)
(:goal
(and
(on b1 b4)
(on b3 b1)
(on b4 b2)
(on b6 b7)
(on b7 b5))
)
)


