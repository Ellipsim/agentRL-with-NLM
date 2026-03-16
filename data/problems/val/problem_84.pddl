

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b9)
(ontable b4)
(on b5 b8)
(on b6 b3)
(ontable b7)
(on b8 b11)
(on b9 b5)
(on b10 b1)
(on b11 b4)
(clear b2)
(clear b6)
(clear b7)
(clear b10)
)
(:goal
(and
(on b1 b5)
(on b4 b7)
(on b5 b2)
(on b6 b4)
(on b7 b10)
(on b9 b8)
(on b10 b1)
(on b11 b6))
)
)


