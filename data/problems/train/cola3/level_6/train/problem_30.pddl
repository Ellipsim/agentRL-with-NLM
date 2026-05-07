

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b7)
(ontable b4)
(on b5 b6)
(on b6 b3)
(on b7 b2)
(clear b1)
(clear b4)
(clear b5)
)
(:goal
(and
(on b1 b4)
(on b2 b3)
(on b6 b7)
(on b7 b5))
)
)


