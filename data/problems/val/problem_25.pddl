

(define (problem BW-rand-5)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(on b1 b3)
(ontable b2)
(ontable b3)
(on b4 b2)
(ontable b5)
(clear b1)
(clear b4)
(clear b5)
)
(:goal
(and
(on b1 b3)
(on b2 b1)
(on b4 b2)
(on b5 b4))
)
)


