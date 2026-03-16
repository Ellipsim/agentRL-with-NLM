

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(ontable b3)
(on b4 b10)
(on b5 b2)
(on b6 b1)
(on b7 b6)
(on b8 b3)
(on b9 b5)
(on b10 b8)
(clear b4)
(clear b7)
(clear b9)
)
(:goal
(and
(on b1 b4)
(on b2 b7)
(on b3 b10)
(on b6 b3)
(on b7 b1)
(on b9 b2)
(on b10 b9))
)
)


