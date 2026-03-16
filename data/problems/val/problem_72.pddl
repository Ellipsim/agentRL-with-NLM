

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(ontable b3)
(ontable b4)
(on b5 b3)
(on b6 b4)
(ontable b7)
(clear b1)
(clear b5)
(clear b6)
(clear b7)
)
(:goal
(and
(on b2 b6)
(on b5 b7)
(on b6 b5)
(on b7 b3))
)
)


