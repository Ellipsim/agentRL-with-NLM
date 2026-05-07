

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(ontable b3)
(on b4 b2)
(ontable b5)
(on b6 b3)
(on b7 b5)
(clear b1)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b2)
(on b4 b3)
(on b5 b6)
(on b6 b7))
)
)


